import utils
from convertEbook import Config, main


def build_param():
    import argparse
    parser = argparse.ArgumentParser(description='convert-ebook')
    parser.add_argument('source', type=str, default=None,
                        help="specify file or dir")
    parser.add_argument('-E', '--epub_version', type=str,
                        default="2",
                        help="specify EPUB version to unpack to: 2, 3 or A (for automatic) or F for Force to EPUB2, default is 2")
    args = parser.parse_args()
    config = Config()

    config.source = args.source
    config.epub_version = args.epub_version
    return config


config = build_param()
config.bundle_dir = utils.get_bundle_dir()
config.tmp_dir = utils.get_tmp_dir()
config.kindlegen_bin = utils.kindle_gen_bin(config.bundle_dir)
print(config)
main(config)
