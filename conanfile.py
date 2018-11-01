from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class FreetypeConan(ConanFile):
    name = "freetype"
    version = "2.9.0"
    description = "FreeType is a freely available software library to render fonts."
    url = "https://github.com/conanos/freetype"
    homepage = "https://www.freetype.org"
    license = "BSD"
    exports = ['LICENSE.md']
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    requires = "zlib/1.2.11@conanos/dev", "bzip2/1.0.6@conanos/dev", "libpng/1.6.34@conanos/dev"

    source_subfolder = "source_subfolder"
    
    def source(self):
        source_url = "https://download.savannah.gnu.org/releases/"
        version = self.version[:-2]
        archive_file = '{0}-{1}.tar.gz'.format(self.name, version)
        source_file = '{0}/{1}/{2}'.format(source_url, self.name, archive_file)
        tools.get(source_file)
        os.rename('{0}-{1}'.format(self.name, version), self.source_subfolder)

    def build(self):
        with tools.chdir(self.source_subfolder):
            with tools.environment_append(
                {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
                %(self.deps_cpp_info["zlib"].rootpath,
                self.deps_cpp_info["bzip2"].rootpath,
                self.deps_cpp_info["libpng"].rootpath)}):

                _args = ['--prefix=%s/builddir'%(os.getcwd()), '--libdir=%s/builddir/lib'%(os.getcwd()), '--with-harfbuzz=no']
                if self.options.shared:
                    _args.extend(['--enable-shared=yes','--enable-static=no'])
                else:
                    _args.extend(['--enable-shared=no','--enable-static=yes'])
                self.run('./configure %s'%(' '.join(_args)))#space
                self.run('make -j2')
                self.run('make install')

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

