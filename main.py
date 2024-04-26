from entail_engine import tt_entails
from expr import kb2expr, expr

if __name__ == '__main__':
    kb = ['It_is_raining & ~I_have_an_umbrella => I_get_wet', 'It_is_raining']
    query = 'I_get_wet'
    print(tt_entails(kb2expr(kb), expr(query)))
