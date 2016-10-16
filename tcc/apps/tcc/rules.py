import rules

@rules.predicate
def is_manager(user):
    return user.is_staff

@rules.predicate
def not_self(user, employee):
    return user.pk != employee.user.pk

@rules.predicate
def not_team_member(user, team):
    return not user.employee.team_set.filter(id=team.pk).exists()

rules.add_rule('user.can_see_profile', is_manager)
rules.add_rule('user.can_make_progress_feedback', is_manager)
rules.add_rule('user.can_make_task_feedback', not_self)
rules.add_rule('team.can_receive_feedback_from', is_manager | not_team_member)
