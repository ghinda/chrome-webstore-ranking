'use strict'

module.exports = function (grunt) {
    // load all grunt tasks
    require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

    var jsDeps = {
        public: [
            'bower_components/jquery/jquery.js',
            'bower_components/bootstrap/dist/js/bootstrap.js',
            'bower_components/modernizr/modernizr.js',

            'bower_components/d3/d3.js',
            'bower_components/nvd3/build/nv.d3.js',

            'js/main.js'
        ]
    };

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        concat: {
            public: {
                src: jsDeps.public,
                dest: 'js/_index.js'
            }
        },
        jshint: {
            dev: [
                'js/main.js'
            ],
            options: {
                multistr: true
            }
        },
        less: {
            development: {
                options: {
                    'paths': ['css/']
                },
                files: {
                    'css/main.css': 'css/main.less'
                }
            }
        },
        watch: {
            scripts: {
                files: ['js/main.js'],
                tasks: ['jshint', 'concat'],
                options: {
                    spawn: false,
                    livereload: 1337
                }
            },
            styles: {
                files: ['css/*.less'],
                tasks: ['less'],
                options: {
                    spawn: false,
                    livereload: 1337
                }
            }
        },
        // Put files not handled in other tasks here
        copy: {
        }
    });

    // Default task(s).
    grunt.registerTask('js', ['jshint', 'concat']);
    grunt.registerTask('css', ['less']);
    grunt.registerTask('default', ['js', 'css', 'watch']);
};
