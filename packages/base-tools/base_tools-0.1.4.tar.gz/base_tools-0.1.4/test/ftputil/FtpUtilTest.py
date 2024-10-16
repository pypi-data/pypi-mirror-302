import unittest

from src.cjlutils import FtpUtil


class CreateDirectoryIfNotExistsTestCase(unittest.TestCase):
    HOST = "10.219.25.127"
    PORT = 21
    USER = "uploader"
    PASSWORD = "uploader"

    def test_something(self):
        version = '9.19.0'
        git = '3a859ebad'

        base_dir = '/IM-Native/iOS'
        dir9 = f'{base_dir}/{version}_{git}'
        ftp = FtpUtil.connect_remote_computer(self.HOST, self.PORT, self.USER, self.PASSWORD)
        FtpUtil.create_directory_if_not_exists(ftp, dir9)

        base_local_dir = '/Users/chenjili/Downloads/9.19.0'
        file_names = [
            'NIMTool_v9.19.0_3a859ebad.ipa',
            'NIM_iOS_SDK_v9.19.0_3a859ebad.zip',
            'NIM_v9.19.0_3a859ebad.ipa',
            'NIM_iOS_SDK_IM_v9.19.0_3a859ebad.zip',
        ]
        for file_name in file_names:
            FtpUtil.upload_file_directly(ftp, f'{base_local_dir}/{file_name}', f'{dir9}/{file_name}')
        print(FtpUtil.ls(ftp, dir9))
        FtpUtil.close(ftp)

    def test_cwd(self):
        version = '9.19.0'
        git = '3a859ebad'
        base_dir = '/IM-Native/iOS'
        dir9 = f'{base_dir}/{version}_{git}'
        ftp = FtpUtil.connect_remote_computer(self.HOST, self.PORT, self.USER, self.PASSWORD)
        print(ftp.pwd())
        ftp.cwd(dir9)
        print(ftp.pwd())
        FtpUtil.close(ftp)


if __name__ == '__main__':
    unittest.main()
