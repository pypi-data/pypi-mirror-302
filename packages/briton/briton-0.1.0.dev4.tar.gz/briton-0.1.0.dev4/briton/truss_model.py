import os
from itertools import count
from pathlib import Path
from typing import cast

import briton.briton_pb2
import briton.briton_pb2_grpc
import grpc
from transformers import AutoTokenizer, PreTrainedTokenizerFast
from briton.briton import BritonInteractor, BritonInteractorImpl
from briton.checks import trllm_config_check
from briton.constants import DEFAULT_MAX_FSM_WORKERS, DEFAULT_BRITON_PORT, FSM_CACHE_DIR, MODEL_INPUT_TO_BRITON_FIELD, OPENAI_COMPATIBLE_TAG, TOOL_CALL_TOKENS
from briton.fsm_cache import FsmCache
from briton.trtllm_build_config import TrussTRTLLMBuildConfiguration
from briton.secrets import get_hf_token_or_none
from briton.schema import ModelInput, create_completion, create_completion_chunks
from briton.error_handling import grpc_error_handling
from briton.constants import TOOL_CALL_IDS

import fastapi
from fastapi import HTTPException


class Model:
    def __init__(self, **kwargs):
        self._loaded = False
        self._model = None
        self._config = kwargs["config"]
        self._data_dir = kwargs["data_dir"]
        self._stub = None
        self._secrets = kwargs["secrets"]
        self._request_id_counter = count(start=1)
        self._briton_process = None
        model_metadata = self._config.get("model_metadata", {})
        tags = model_metadata.get("tags", [])
        if OPENAI_COMPATIBLE_TAG not in tags:
            self._openai_compatible = False
        else:
            self._openai_compatible = True

        trllm_config_check(self._config)
        trtllm_config = self._config.get("trt_llm")
        truss_trtllm_build_config = TrussTRTLLMBuildConfiguration(
            **trtllm_config.get("build")
        )
        self._base_model = truss_trtllm_build_config.base_model
        self._tp_count = truss_trtllm_build_config.tensor_parallel_count
        self._tokenizer_repository = (
            truss_trtllm_build_config.checkpoint_repository.repo
        )
        self._kv_cache_free_gpu_mem_fraction = (
            truss_trtllm_build_config.kv_cache_free_gpu_mem_fraction
        )
        self._enable_kv_cache_reuse = (
            truss_trtllm_build_config.plugin_configuration.use_paged_context_fmha
        )
        self._enable_chunked_context = truss_trtllm_build_config.enable_chunked_context

        self._max_input_len = truss_trtllm_build_config.max_input_len
        self._max_beam_width = truss_trtllm_build_config.max_beam_width
        self._max_num_tokens = truss_trtllm_build_config.max_num_tokens

        self._hf_token = get_hf_token_or_none(self._secrets)

        # TODO(@bdubayah): configure this based on CPU. But os.cpu_count() returns the
        # number of CPUs for the entire node, not just the container.
        self._max_fsm_workers = DEFAULT_MAX_FSM_WORKERS
        print(f"Using {self._max_fsm_workers} workers for FSM schema generation")
        # Allow passing briton_interactor for ease of testing
        self._briton_interactor: BritonInteractor = \
          model_metadata.get("briton_interactor", BritonInteractorImpl())
        self._tool_call_token = TOOL_CALL_TOKENS.get(self._base_model)
        self._tool_call_token_id = TOOL_CALL_IDS.get(self._base_model)

    def load(self):
        if self._loaded:
            return

        # TODO(pankaj) Support loading bundled tokenizer rather than from HF
        self._tokenizer = AutoTokenizer.from_pretrained(
            self._tokenizer_repository, token=self._hf_token
        )

        self._fsm_cache = FsmCache(
            Path(FSM_CACHE_DIR), self._tokenizer, self._max_fsm_workers, self._tool_call_token_id
        )

        # We only support Llama and mistral with Briton, for which this should
        # apply.
        assert isinstance(self._tokenizer, PreTrainedTokenizerFast)

        # These are tokens outside of tokenizer.json. We need to pass these to
        # Briton, to pass to rust tokenizer.
        added_token_decoders = self._tokenizer.added_tokens_decoder
        added_tokens = [token for token in added_token_decoders.values()]

        load_briton = self._briton_interactor.load
        load_briton(
            model_name="briton",
            engine_path=self._data_dir,
            hf_tokenizer=self._tokenizer_repository,
            work_dir=self._data_dir,
            fsm_cache_dir=self._fsm_cache.cache_dir,
            kv_cache_free_gpu_mem_fraction=self._kv_cache_free_gpu_mem_fraction,
            port=DEFAULT_BRITON_PORT,
            added_tokens=added_tokens,
            max_num_tokens=self._max_num_tokens,
            enable_chunked_context=self._enable_chunked_context,
            hf_token=self._hf_token,
            tp_count=self._tp_count,
        )
        self._loaded = True

    async def predict(self, model_input, request: fastapi.Request):
        #TODO(pankaj) Wire up request cancellation
        """
        Run inference

        Note that the async nature of this function is a little tricky. Care is
        needed to make sure this function is a regular async function and not an
        async generator, i.e. there shouldn't be any direct yields in this
        function. This is because we need to support both streaming and
        non-streaming cases in this function. We do this by either returning an
        async-generator for the streaming case, or directly the full text for
        the other case. Returning an async generator for non-streaming case
        interferes with the open ai client proxy.
        """
        if self._stub is None:
            self._stub = self._briton_interactor.create_grpc_stub(DEFAULT_BRITON_PORT)

        val_model_input = ModelInput(**model_input)
        prompt = val_model_input.prompt(cast(PreTrainedTokenizerFast, self._tokenizer))
        model_input.pop("messages", None)
        
        request_id = self._calc_request_id()
        request = briton.briton_pb2.InferenceRequest(
            request_id=request_id,
            input_text=prompt,
        )
        self._update_request_end_id_pad_id(request, model_input)

        # Add output schema hash if we're function calling or response_format is provided
        schema_hash = None
        schema = val_model_input.output_json_schema
        if schema is not None:
            try:
                schema_hash = await self._fsm_cache.add_schema(schema)
            # If the input schema is invalid, we should return a 400
            except NotImplementedError as ex:
                raise HTTPException(status_code=400, detail=str(ex))
            request.output_schema_hash = schema_hash
            force_tools = val_model_input.force_tools
            if force_tools is not None:
                request.force_tools = force_tools

        # Add renamed fields to the raw dict
        if val_model_input.max_tokens is not None:
            model_input["max_tokens"] = val_model_input.max_tokens
        if val_model_input.top_k is not None:
            model_input["runtime_top_k"] = val_model_input.top_k
        if val_model_input.top_p is not None:
            model_input["runtime_top_p"] = val_model_input.top_p

        set_briton_request_fields_from_model_input(model_input, request)
        for words in ["bad_words", "stop_words"]:
            if words in model_input:
                for word in model_input[words].split(","):
                    getattr(request, words).append(word)

        resp_iter = self._stub.Infer(request)

        model_name = model_input.get("model", "")

        with grpc_error_handling():
            if model_input.get("stream", True):
                async for first_chunk in resp_iter:
                    break

                async def generate_after_first_chunk():
                    yield first_chunk.output_text
                    async for chunk in resp_iter:
                        yield chunk.output_text

                if self._openai_compatible:
                    return create_completion_chunks(
                        req_id=str(request_id),
                        model=model_name,
                        input_text=generate_after_first_chunk(),
                        eos_token=self._eos_token(),
                        tool_token=self._tool_call_token,
                    )
                return generate_after_first_chunk()
            else:
                full_text = await _collect_text(resp_iter)
                if self._openai_compatible:
                    return create_completion(
                        req_id=str(request_id),
                        model=model_name,
                        input_text=full_text,
                        eos_token=self._eos_token(),
                        tool_token=self._tool_call_token
                    )
                return full_text

    def _calc_request_id(self) -> int:
        """Calculate unique request id.

        Not thread safe, but safe to use in single threaded async context. There
        are no async operations here, so this function is unlikely to be
        preempted in the middle. This is important otherwise we may end up with
        duplicate ids.
        """
        return int(str(os.getpid()) + str(next(self._request_id_counter)))

    def _eos_token(self):
        return getattr(self._tokenizer, "eos_token", None)

    def _eos_token_id(self):
        return getattr(self._tokenizer, "eos_token_id", None)

    def _pad_token_id(self):
        return getattr(self._tokenizer, "pad_token_id", None)

    def _update_request_end_id_pad_id(self, request, model_input):
        end_id = model_input.get("end_id", None) or self._eos_token_id()
        if end_id is not None:
            request.end_id = end_id
        pad_id = model_input.get("pad_id", None) or self._pad_token_id() 
        if pad_id is not None:
            request.pad_id = pad_id


def set_briton_request_fields_from_model_input(model_input, briton_request):
    for model_input_key, briton_field in MODEL_INPUT_TO_BRITON_FIELD.items():
        if model_input_key in model_input:
            model_input_value = model_input[model_input_key]
            setattr(briton_request, briton_field, model_input_value)


async def _collect_text(async_text_iter):
    full_text = ""
    async for delta in async_text_iter:
        full_text += delta.output_text
    return full_text
