import unittest

from src.cjlutils import SoundUtil, FileUtil


class CreateWaveTestCase(unittest.TestCase):
    def test_the_second_walt(self):
        sample_rate = 44100
        g1 = SoundUtil.get_frequency_by_clef(SoundUtil.ClefTypeEnum.TREBLE, 1,
                                             SoundUtil.get_average_12_order(SoundUtil.SolmizationEnum.SOL))
        be = SoundUtil.get_frequency_by_clef(SoundUtil.ClefTypeEnum.TREBLE, 1,
                                             SoundUtil.get_average_12_order(SoundUtil.SolmizationEnum.MI, -1))
        d = SoundUtil.get_frequency_by_clef(SoundUtil.ClefTypeEnum.TREBLE, 1,
                                            SoundUtil.get_average_12_order(SoundUtil.SolmizationEnum.RE))
        c = SoundUtil.get_frequency_by_clef(SoundUtil.ClefTypeEnum.TREBLE, 1,
                                            SoundUtil.get_average_12_order(SoundUtil.SolmizationEnum.DO))

        speed = 174
        arr = list(SoundUtil.create_wave(g1, 3 * 60 / speed, sample_rate=sample_rate))
        arr += list(SoundUtil.create_wave(be, 2 * 60 / speed, sample_rate=sample_rate))
        arr += list(SoundUtil.create_wave(d, 1 * 60 / speed, sample_rate=sample_rate))
        arr += list(SoundUtil.create_wave(c, 3 * 60 / speed, sample_rate=sample_rate))
        FileUtil.create_audio_file(arr, './audio/sound.wav', sample_rate=sample_rate)
        print('done')


if __name__ == '__main__':
    unittest.main()
