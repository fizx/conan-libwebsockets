from conans import ConanFile, tools, CMake
import os
import shutil

class LibwebsocketsConan(ConanFile):
    name = "LibWebsockets"
    version = "2.1"
    settings = "os", "compiler", "build_type", "arch"
    exports = "CMakeLists.txt"
    generators = "cmake", "txt"

    def config(self):
        self.requires.add("OpenSSL/1.0.2h@lasote/stable", private=False)
        self.requires.add("LibUV/1.x@fizx/testing")

    def source(self):
        self.run("git clone https://github.com/warmcat/libwebsockets.git")
        shutil.move("libwebsockets/CMakeLists.txt", "libwebsockets/CMakeListsOriginal.cmake")
        shutil.move("CMakeLists.txt", "libwebsockets/CMakeLists.txt")

    def build(self):
        cmake = CMake(self.settings)
        cmake_options = []
        self.options["OpenSSL"].shared = False
        for option_name in self.options.values.fields:
            activated = getattr(self.options, option_name)
            the_option = "%s=" % option_name.upper()
            cmake_options.append(the_option)
            
        cmake_options.append("LWS_WITH_LIBUV=1")

        options_lws = " -D".join(cmake_options)
        conf_command = 'cd libwebsockets && cmake %s -D%s' % (cmake.command_line, options_lws)
        
        self.output.warn(conf_command)
        self.run(conf_command)

        self.run("cmake --build libwebsockets %s" % cmake.build_config)
        
        # cmake -DLWS_WITH_LIBUV=1 -DLWS_WITH_HTTP2=1 -DLWS_OPENSSL_INCLUDE_DIRS=/usr/local/opt/openssl/include -DLWS_OPENSSL_LIBRARIES="/usr/local/opt/openssl/lib/libssl.a;/usr/local/opt/openssl/lib/libcrypto.a"  ..
        
    def package(self):
        self.copy("*.h", dst="include", src="libuv-v1.9.1/include")
        self.copy("*", dst="lib", src="libuv-v1.9.1/.libs")

    def package_info(self):
        self.cpp_info.libs = ["uv"]
        
        
        # DLWS_WITH_LIBUV=1 -DLWS_WITH_HTTP2=1