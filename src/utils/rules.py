def first_rule_open(first_point, second_point):
    return all([first_point.frame[1].close >= first_point.frame[1].open,
                first_point.frame[1].open*(1-0.0003) <= second_point.frame[1].high])


def second_rule_open(first_point, second_point):
    return all([first_point.frame[1].close <= first_point.frame[1].open,
                first_point.frame[1].open*(1-0.0003) <= second_point.frame[1].high])


def first_rule_close(first_point, second_point):
    return all([first_point.frame[1].close > first_point.frame[1].open,
                first_point.frame[1].open*(1+0.0005) >= second_point.frame[1].low])


def second_rule_close(first_point, second_point):
    return all([first_point.frame[1].close <= first_point.frame[1].open,
                first_point.frame[1].close*(1+0.0005) >= second_point.frame[1].low])