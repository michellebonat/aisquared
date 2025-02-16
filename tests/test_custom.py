import pytest
import aisquared


def test_custom():
    obj = aisquared.base.CustomObject(
        'TestClass',
        test='foo',
        otherTest='bar'
    )
    assert obj.to_dict() == {
        'className': 'TestClass',
        'params': {
            'test': 'foo',
            'otherTest': 'bar'}
    }
    assert obj.path is None
