
from checks import AgentCheck
from checks.check_status import STATUS_OK, STATUS_ERROR, InstanceStatus, CheckStatus, CollectorStatus
import nose.tools as nt


class DummyAgentCheck(AgentCheck):

    def check(self, instance):
        if not instance['pass']:
            raise Exception("failure")



def test_check_status_fail():
    instances = [
        {'pass':True},
        {'pass':False},
        {'pass':True}
    ]
        
    check = DummyAgentCheck('dummy_agent_check', {}, {}, instances)
    instance_statuses = check.run()
    assert len(instance_statuses) == 3
    assert instance_statuses[0].status == STATUS_OK
    assert instance_statuses[1].status == STATUS_ERROR
    assert instance_statuses[2].status == STATUS_OK
        

def test_check_status_pass():
    instances = [
        {'pass':True},
        {'pass':True},
    ]
        
    check = DummyAgentCheck('dummy_agent_check', {}, {}, instances)
    instances_status = check.run()
    assert len(instances_status) == 2
    for i in instances_status:
        assert i.status == STATUS_OK

def test_persistence():
    i1 = InstanceStatus(1, STATUS_OK)
    chk1 = CheckStatus("dummy", [i1])
    c1 = CollectorStatus([chk1])
    c1.persist()

    c2 = CollectorStatus.load()
    nt.assert_equal(1, len(c2.check_statuses))
    chk2 = c2.check_statuses[0]
    assert chk2.name == chk1.name
    assert chk2.status == chk2.status

def test_persistence_fail():
    import os
    os.remove(CollectorStatus._get_pickle_path())
    nt.assert_raises(Exception, CollectorStatus.load)
