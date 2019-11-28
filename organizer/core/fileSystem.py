from .config import Config
import os
import shutil
from .common import InputError


class FileSystem:
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.search_directories = self.config.getConfigValue(
            "search_directories", "filesystem")
        self.staging_directory = self.config.getConfigValue(
            "staging_directory", "filesystem")
        self.image_extensions = self.config.getConfigValue(
            "image_extensions", "filesystem")
        self.video_extensions = self.config.getConfigValue(
            "video_extensions", "filesystem")
        self.audio_extensions = self.config.getConfigValue(
            "audio_extensions", "filesystem")

    def getResolution(self, filename):
        """This function finds the resolution of the image file it is passed"""
        return filename

    def printSearchDirs(self):
        print(self.search_directories)
        return

    def printPropValues(self):
        print(self.__dict__)
        return

    def checkVideos(self):
        self.search_videos = self.config.getConfigValue(
            "organize_videos", "filesystem")
        return self.search_videos

    def checkAudios(self):
        self.search_audios = self.config.getConfigValue(
            "organize_audios", "filesystem")
        return self.search_audios

    def getTypeStagingDirName(self, mediaType):
        return self.config.getConfigValue(mediaType + "_staging_dir_name", "filesystem")

    def checkOrCreateStaging(self, mediaType):
        if not os.path.exists(self.staging_directory):
            os.makedirs(os.path.join(self.staging_directory,
                                     self.getTypeStagingDirName(mediaType)))
        return

    def checkOrCreatePhotoOrganizerFolder(self, mediaType):
        if mediaType == 'images':
            self.root_images_directory = self.config.getConfigValue(
                "root_images_directory", "filesystem")
            self.root_images_directory = os.path.join(
                self.root_images_directory, self.config.getConfigValue("root_images_directory_name", "filesystem"))
            if not os.path.exists(self.root_images_directory):
                os.makedirs(self.root_images_directory)
        elif mediaType == 'videos':
            self.root_videos_directory = self.config.getConfigValue(
                "root_videos_directory", "filesystem")
            self.root_videos_directory = os.path.join(
                self.root_videos_directory, self.config.getConfigValue("root_videos_directory_name", "filesystem"))
            if not os.path.exists(self.root_videos_directory):
                os.makedirs(self.root_videos_directory)
        elif mediaType == 'audios':
            self.root_audios_directory = self.config.getConfigValue(
                "root_audios_directory", "filesystem")
            self.root_audios_directory = os.path.join(
                self.root_audios_directory, self.config.getConfigValue("root_audios_directory_name", "filesystem"))
            if not os.path.exists(self.root_audios_directory):
                os.makedirs(self.root_audios_directory)
        else:
            raise InputError("mediaType", "MediaType input is not allowed!")
        return

    def removeStagingDirs(self):
        if os.path.exists(self.staging_directory):
            shutil.rmtree(self.staging_directory)
        return

    def addSearchExtension(self, ext, mediaType):
        if mediaType == 'images':
            self.image_extensions.append(ext)
            self.config.writeConfig(
                "filesystem", "image_extensions", self.image_extensions)
        elif mediaType == 'videos':
            self.video_extensions.append(ext)
            self.config.writeConfig(
                "filesystem", "video_extensions", self.video_extensions)
        elif mediaType == 'audios':
            self.audio_extensions.append(ext)
            self.config.writeConfig(
                "filesystem", "audio_extensions", self.audio_extensions)
        else:
            raise InputError("mediaType", "MediaType input is not allowed!")
        return

    def removeSearchExtension(self, ext, mediaType):
        if mediaType == 'images':
            self.image_extensions.remove(ext)
            self.config.writeConfig(
                "filesystem", "image_extensions", self.image_extensions)
        elif mediaType == 'videos':
            self.video_extensions.remove(ext)
            self.config.writeConfig(
                "filesystem", "video_extensions", self.video_extensions)
        elif mediaType == 'audios':
            self.audio_extensions.remove(ext)
            self.config.writeConfig(
                "filesystem", "audio_extensions", self.audio_extensions)
        else:
            raise InputError("mediaType", "MediaType input is not allowed!")
        return

    def findAllFiles(self, mediaType):
        print("Finding files by extension")
        files = []
        for dir in self.search_directories:
            if mediaType == 'images':
                images = self.searchDirectory(dir, self.image_extensions)
                files.extend(images)
            elif mediaType == 'videos':
                videos = self.searchDirectory(dir, self.video_extensions)
                files.extend(videos)
            elif mediaType == 'audios':
                audios = self.searchDirectory(dir, self.audio_extensions)
                files.extend(audios)
            else:
                raise InputError(
                    "mediaType", "MediaType input is not allowed!")
        print("Files: %s" % (files))
        return files

    def searchDirectory(self, folder, extensions):
        print("Searching %s for extensions: %s" % (folder, extensions))
        mediaFiles = []
        for root, directories, files in os.walk(folder):
            for name in files:
                filename, fileext = os.path.splitext(name)
                if fileext[1:] in extensions:
                    mediaFiles.append(os.path.join(root, name))
        return mediaFiles

    def moveFilesToStaging(self, files, mediaType):
        print("Moving files now")
        mediaStagingDir = os.path.join(
            self.staging_directory, self.getTypeStagingDirName(mediaType))
        for f in files:
            os.rename(f, os.path.join(mediaStagingDir, os.path.basename(f)))
        for dir in self.search_directories:
            self.removeEmptyDirectories(dir)
        return

    def removeEmptyDirectories(self, folder):
        for root, directories, files in os.walk(folder):
            for dir in directories:
                try:
                    print("Trying to remove directory: %s" %
                          os.path.join(root, dir))
                    os.rmdir(os.path.join(root, dir))
                except OSError as ex:
                    print(ex)
        return
