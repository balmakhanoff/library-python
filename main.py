from app.dict_questions import questions
from app.crud_operations import Operations
from app.utils import logger


def main(is_running: str = False) -> None:
    operations = Operations()

    while is_running:
        print(questions['main_menu'])
        question: str = str(input('Choose number of menu(for example "3"): '))

        try:
            if question == '1':
                operations.add_book()

            elif question == '2':
                operations.delete_book()

            elif question == '3':
                operations.show_books()

            elif question == '4':
                operations.search_the_book()

            elif question == '5':
                operations.change_book_status()

            elif question.lower() == 'exit' or question == '6':
                is_running = False
            else:
                print('Not correct answer, please choose again.')
                logger('Choosen operation # ' + question, 'info')

        except Exception as err:
            logger(err, 'error')


if __name__ == '__main__':
    main(is_running=True)
