import rules

@rules.predicate
def is_manager(user):
    return user.is_staff

@rules.predicate
def not_self(user, employee):
    return user.pk != employee.user.pk

rules.add_rule('user.can_see_profile', is_manager)
rules.add_rule('user.can_make_progress_feedback', is_manager)
rules.add_rule('user.can_make_task_feedback', not_self)
