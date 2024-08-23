const path = require('path');
const { styles } = require( '@ckeditor/ckeditor5-dev-utils' );
const { CKEditorTranslationsPlugin } = require( '@ckeditor/ckeditor5-dev-translations' );
const MiniCssExtractPlugin = require( 'mini-css-extract-plugin' );

module.exports = {
    entry: {
        base: [
            './df_site_js/base.ts',
            './df_site_js/base.scss',
        ],
        app: [
            './df_site_js/app.ts',
            './df_site_js/app.scss'
        ]
    },
    resolve: {
        extensions: ['.ts', '.js']
    },
    output: {
        filename: 'js/[name].js',
        path: path.resolve(__dirname, 'df_site/static'),
    },
    optimization: {
        minimize: false
    },
    plugins: [
        new CKEditorTranslationsPlugin( {
            // The main language that will be built into the main bundle.
            language: 'fr',

            // Additional languages that will be emitted to the `outputDirectory`.
            // This option can be set to an array of language codes or `'all'` to build all found languages.
            // The bundle is optimized for one language when this option is omitted.
            additionalLanguages: 'all',
            addMainLanguageTranslationsToAllAssets: true,

            // For more advanced options see https://github.com/ckeditor/ckeditor5-dev/tree/master/packages/ckeditor5-dev-translations.
        } ),
        new MiniCssExtractPlugin( {
            filename: 'css/ckeditor5.css'
        } )
    ],
    module: {
        rules: [
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/i,
                type: 'asset/resource',
                generator: {filename: 'webfonts/[name][ext][query]'},
            },
            {
                test: /\.c?js$/,
                enforce: "pre",
                use: ["source-map-loader"],
            },
            {
                test: /\.ts$/,
                use: 'ts-loader',
                exclude: /node_modules/
            },
            {
                test: /\.(png|jpg|jpeg|gif)$/,
                type: 'asset/resource',
                generator: {filename: 'images/[name][ext][query]'},
            },
            {
                test: /\.(svg)$/,
                use: [ 'raw-loader' ],
            },
                      {
                test: /\.css$/,

                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    {
                        loader: 'postcss-loader',
                        options: {
                            postcssOptions: styles.getPostCssConfig( {
                                themeImporter: {
                                    themePath: require.resolve( '@ckeditor/ckeditor5-theme-lark' )
                                },
                                minify: true
                            } )
                        }
                    }
                ]
            },

            {
                test: /\.scss$/,
                exclude: /node_modules/,
                type: 'asset/resource',
                generator: {filename: 'css/[name].css[query]'},
                use: [{loader: 'sass-loader', options: {sourceMap: true,}}]
            }
        ]
    },
    // Useful for debugging.
    devtool: 'source-map',
    performance: {hints: false}
}
/*
module.exports = {
    entry: {
        base: [
            './df_site_js/base.ts',
            './df_site_js/base.scss',
        ],
        app: [
            './df_site_js/app.ts',
            './df_site_js/app.scss'
        ]
    },
    devtool: 'source-map',
    output: {
        filename: 'js/[name].js',
        path: path.resolve(__dirname, 'df_site/static'),
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
                generator: {
                    filename: 'js/[name].js[query]',
                },
            },
            {
                test: /\.scss$/,
                exclude: /node_modules/,
                type: 'asset/resource',
                generator: {
                    filename: 'css/[name].css[query]',
                },
                use: [
                    {
                        loader: 'sass-loader', options: {
                            sourceMap: true,
                        },

                    }
                ]
            },
            {
                test: /\.(png|svg|jpg|jpeg|gif)$/i,
                type: 'asset/resource',
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/i,
                type: 'asset/resource',
            },
        ],
    },
    resolve: {
        extensions: ['.ts', '.js'],
    },

};
*/
