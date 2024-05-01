from utils import file_parser


def test_file_parser():
    kb, query = file_parser('data/test_file_parser_txt')
    
    assert kb == ['p2==> p3', 'p3 ==> p1', 'c ==> e', 'b&e ==> f', 'f&g ==> h', 'p2&p1&p3==>d', 'p1&p3 ==> c', 'a', 'b', 'p2']
    assert query == 'd'
