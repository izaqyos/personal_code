module.exports = function(grunt) {
	var banner = '/*n<%= pkg.name %> <%= pkg.version %> - <%= pkg.description %>n<%= pkg.repository.url %>nBuilt on <%= grunt.template.today("yyyy-mm-dd") %>n*/n';

        // section 1 - require modules
    require('load-grunt-tasks')(grunt);

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
                eslint: {
            options: {
                config: 'eslint.json',
                reset: true
            },
            target: ['*.js']
        },
        // task for mocha tests execution, they would be executed by nyc
        mochaTest: {
            local: {
                options: {
                    reporter: 'spec'
                },
                src: ['test/*.js']
            }
        },
        // nyc - executes mochaTest task
        nyc: {
            local: {
                options: {
                    all: true,
                    exclude: [
                        "**/*.spec.js",
                        "**/Gruntfile.js",
                        "**/Mock*",
                        "**/coverage",
                        "**/resources"
                    ],
                    reporter: ['text-summary', 'html'],
                    checkCoverage: true,
                    lines: 90
                },
                cmd: false,
                args: ['grunt', 'mochaTest:local', '--force']
            }
        }
	});


// section 3 - register grunt tasks
        //    grunt.loadNpmTasks('gruntify-eslint');
    grunt.loadNpmTasks('grunt-mocha-test');
    grunt.loadNpmTasks('grunt-simple-nyc');

    // Default task
    //grunt.registerTask('default', [ 'test']);
    grunt.registerTask('default', ['lint', 'test']);
    // Lint task
    //grunt.registerTask('lint', ['eslint:ci']);
    grunt.registerTask('lint', ['eslint']);
    // Mocha test task
    grunt.registerTask('test', ['nyc:local']);
};

