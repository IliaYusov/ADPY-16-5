import re
import csv
from pprint import pprint


def split_names(contact):
    full_name = f'{contact[0]} {contact[1]} {contact[2]}'.split()
    return full_name[0], full_name[1], (full_name[2:3] + [''])[0]


def phone_regex(contact):
    phone_pattern = re.compile(
        r"\+?[78]\s*\(?(\d{3})\)?\s*-?\s*(\d{3})\s*-?\s*(\d{2})\s*-?\s*(\d{2})\s*\(?\s*(?:доб)?\.?\s*(\d*)")
    phone = re.match(phone_pattern, contact[5])
    if phone:
        return f'+7({phone[1]}){phone[2]}-{phone[3]}-{phone[4]}{" доб." + phone[5] if phone[5] else ""}'
    else:
        return


def join_doubles(index_new, index_old, contacts):
    result = []
    for item_new, item_old in zip(contacts[index_new], contacts[index_old]):
        if item_new == item_old or item_old == '':
            result.append(item_new)
        elif item_new == '':
            result.append(item_old)
        else:
            print('Can`t merge lines:', contacts[index_new], contacts[index_old], sep='\n')
            return
    return result


def main(contacts):
    index_dict = {}
    new_contacts = []
    for index, contact in enumerate(contacts):
        # 1
        contact[0], contact[1], contact[2] = split_names(contact)
        # 2
        phone_number = phone_regex(contact)
        if phone_number:
            contact[5] = phone_number
        # 3
        full_name = contact[0] + " " + contact[1]
        if full_name in index_dict and join_doubles(index, index_dict[full_name]['old'], contacts):
            new_contacts[index_dict[full_name]['new']] = \
                join_doubles(index, index_dict[full_name]['old'], contacts)
        else:
            index_dict[full_name] = {'old': index, 'new': len(new_contacts)}
            new_contacts.append(contact)
    return new_contacts


if __name__ == '__main__':
    with open("phonebook_raw.csv", 'r', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    new_contacts_list = main(contacts_list)

    with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(new_contacts_list)
