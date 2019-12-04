

def check_passwd(passwd):
    occ_list = [1]
    prev = passwd % 10
    passwd = passwd // 10
    for i in range(len(str(passwd))):
        current = passwd % 10
        passwd = passwd // 10
        if prev < current:
            return False
        if prev == current:
            occ_list[-1] += 1
        else:
            occ_list += [1]
        prev = current
    # print(occ_list)
    return 2 in occ_list


def main():
    passwd_min = 245318
    passwd_max = 765747
    # print(check_passwd(1111))
    print(sum(check_passwd(passwd)
              for passwd in range(passwd_min, passwd_max + 1)))


if __name__ == "__main__":
    main()
