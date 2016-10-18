import rules

@rules.predicate
def is_manager(user):
    return user.is_staff

@rules.predicate
def not_self(user, employee):
    return user.pk != employee.user.pk

@rules.predicate
def many_members(user, team):
    return team.members.count() > 1

@rules.predicate
def team_member(user, team):
    return user.employee.team_set.filter(id=team.pk).exists()

rules.add_rule('can_see_profile', is_manager)
rules.add_rule('can_make_progress_feedback', is_manager)
rules.add_rule('can_make_task_feedback', not_self)
rules.add_rule('can_give_team_feedback', is_manager | ~team_member)
rules.add_rule('can_give_team_member_feedback', team_member & many_members)
rules.add_perm('tcc.receive_peer_feedback_team', team_member & many_members)
