"""
Class wrapping :obj:`gwpy.spectrogram.spectrogram.Spectrogram` from GWpy

Authors:
    | Artem Basalaev <artem[dot]basalaev[at]pm.me>
"""
import copy
import gwpy.spectrogram
import gwpy.frequencyseries
import gwpy.timeseries


class Spectrogram(gwpy.spectrogram.Spectrogram):
    """
    Class wrapping :obj:`gwpy.spectrogram.spectrogram.Spectrogram` from GWpy

    """

    @classmethod
    def from_other(cls, sgram):
        """Create Spectrogram from another Spectrogram, in particular gwpy.Spectrogram

        Parameters
        ----------
        sgram : Spectrogram, gwpy.Spectrogram
            Other Spectrogram object
        Returns
        -------
        Spectrogram
            Copy Spicypy Spectrogram object
        """
        sgram_spicypy = cls(sgram.value)
        sgram_spicypy.__dict__ = copy.deepcopy(sgram_spicypy.__dict__)
        return sgram_spicypy

    def _wrap_function(self, *args, **kwargs):
        """Wrap the wrap function from gwpy.Spectrogram, to return Spicypy objects"""
        out = super()._wrap_function(*args, **kwargs)
        if isinstance(out, gwpy.frequencyseries.FrequencySeries):
            # convert to Spicypy object
            from spicypy.signal import FrequencySeries

            return FrequencySeries.from_other(out)
        elif isinstance(out, gwpy.timeseries.TimeSeries):
            # convert to Spicypy object
            from spicypy.signal import TimeSeries

            return TimeSeries.from_other(out)
