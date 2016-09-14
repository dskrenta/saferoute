import riot  from 'rollup-plugin-riot';
import babel from 'rollup-plugin-babel';
import nodeResolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs';
import uglify from 'rollup-plugin-uglify';
import { minify } from 'uglify-js';

export default {
  entry: "public/main.js",
  dest: "public/dist/bundle.js",
  plugins: [
    riot({
      include: 'public/components/**/*.tag'
    }),
    nodeResolve({
      jsnext: true,
      main: true,
      browser: true
    }),
    commonjs(),
    babel({
      env: 'frontend',
      presets: ['es2015-rollup'],
      plugins: [
        'transform-async-to-generator',
        'syntax-async-functions'
      ],
      ignore: 'public/components/**/*.tag'
    }),
    uglify({}, minify)
  ]
}
