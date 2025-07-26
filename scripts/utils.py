import os
# scripts/utils.py

def compare_with_draw(ticket, draw):
    """
    Συγκρίνει ένα δελτίο με την κλήρωση και επιστρέφει πόσα νούμερα ταιριάζουν.
    :param ticket: λίστα με 12 αριθμούς του δελτίου
    :param draw: λίστα με 20 αριθμούς της κλήρωσης
    :return: πλήθος επιτυχιών (int)
    """
    return len(set(ticket) & set(draw))