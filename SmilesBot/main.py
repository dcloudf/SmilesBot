from CGRtools import smiles as SMILES
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Hi! To take a SVG picture of molecule just write /smiles and your smiles string')


def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Help!')


def smiles(update: Update, _: CallbackContext) -> None:
    mol = SMILES(' '.join(_.args))
    mol.canonicalize()
    mol.clean2d()
    with open('mol.svg', 'w') as f:
        f.write(mol.depict())
    update.message.reply_document(document=open('mol.svg', 'rb'))


def main() -> None:
    with open('TOKEN.txt', 'r') as f:
        token_ = f.readline().removesuffix('\n')
    updater = Updater(token_)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler((CommandHandler('smiles', smiles)))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
