from typing import Any, Callable, Iterable, Optional

import torch

from laia.callbacks.meters import SequenceError, char_to_word_seq
from laia.common.arguments import OptimizerArgs, SchedulerArgs
from laia.decoders import CTCGreedyDecoder
from laia.engine import EngineModule
from laia.losses import CTCLoss


class HTREngineModule(EngineModule):
    def __init__(
        self,
        model: torch.nn.Module,
        delimiters: Iterable,
        criterion: Optional[Callable] = CTCLoss(),
        optimizer: OptimizerArgs = OptimizerArgs(),
        scheduler: Optional[SchedulerArgs] = None,
        batch_input_fn: Optional[Callable] = None,
        batch_target_fn: Optional[Callable] = None,
        batch_id_fn: Optional[Callable] = None,
    ):
        super().__init__(
            model,
            criterion,
            optimizer=optimizer,
            scheduler=scheduler,
            batch_input_fn=batch_input_fn,
            batch_target_fn=batch_target_fn,
            batch_id_fn=batch_id_fn,
        )
        self.delimiters = delimiters
        self.decoder = CTCGreedyDecoder()

    def training_step(self, batch: Any, *args, **kwargs):
        result = super().training_step(batch, *args, **kwargs)
        if result is None:
            return
        batch_x, batch_y = self.prepare_batch(batch)
        batch_decode = self.decoder(result["batch_y_hat"])["hyp"]
        cer = torch.tensor(
            SequenceError.compute(batch_y, batch_decode), device=batch_x.device
        )
        self.log(
            "tr_cer",
            cer,
            on_step=False,
            on_epoch=True,
            prog_bar=True,
            sync_dist=True,
        )
        batch_decode_words = [
            char_to_word_seq(b, self.delimiters) for b in batch_decode
        ]
        batch_y_words = [char_to_word_seq(b, self.delimiters) for b in batch_y]
        wer = torch.tensor(
            SequenceError.compute(batch_y_words, batch_decode_words),
            device=batch_x.device,
        )
        self.log(
            "tr_wer",
            wer,
            on_step=False,
            on_epoch=True,
            prog_bar=True,
            sync_dist=True,
        )
        return result

    def validation_step(self, batch: Any, *args, **kwargs):
        result = super().validation_step(batch, *args, **kwargs)
        if result is None:
            return
        batch_x, batch_y = self.prepare_batch(batch)
        batch_decode = self.decoder(result["batch_y_hat"])["hyp"]
        cer = torch.tensor(
            SequenceError.compute(batch_y, batch_decode), device=batch_x.device
        )
        self.log(
            "va_cer",
            cer,
            on_step=False,
            on_epoch=True,
            prog_bar=True,
            sync_dist=True,
        )
        batch_decode_words = [
            char_to_word_seq(b, self.delimiters) for b in batch_decode
        ]
        batch_y_words = [char_to_word_seq(b, self.delimiters) for b in batch_y]
        wer = torch.tensor(
            SequenceError.compute(batch_y_words, batch_decode_words),
            device=batch_x.device,
        )
        self.log(
            "va_wer",
            wer,
            on_step=False,
            on_epoch=True,
            prog_bar=True,
            sync_dist=True,
        )
        return result
