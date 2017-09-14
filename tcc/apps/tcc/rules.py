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


@rules.predicate
def missing_questionnaire(user, team):
    return team.missing_questionnaire(user.employee)


@rules.predicate
def answered_satisfaction_questionnaire(user):
    return user.employee.answered_satisfaction_questionnaire()


@rules.predicate
def has_energy(user):
    return user.employee.energy > 0


@rules.predicate
def is_guest(user):
    return user.employee.is_guest


rules.add_rule('can_see_profile', is_manager)
rules.add_rule('can_make_progress_feedback', is_manager)
rules.add_rule(
    'can_make_task_feedback',
    not_self & ~is_guest & (is_manager | has_energy)
)
rules.add_rule(
    'can_answer_task_feedback',
    ~is_guest & (is_manager | has_energy)
)
rules.add_rule(
    'can_answer_team_task_feedback',
    ~is_guest & (is_manager | has_energy)
)
rules.add_perm(
    'tcc.receive_task_feedback_employee',
    ~is_guest & (is_manager | has_energy)
)
rules.add_perm(
    'tcc.receive_task_feedback_team',
    is_manager | (has_energy & ~is_guest)
)
rules.add_rule('can_answer_satisfaction_quiz', ~is_manager & ~answered_satisfaction_questionnaire)
rules.add_rule('can_give_progress_feedback', is_manager)
rules.add_rule('can_give_team_feedback', is_manager | (~team_member & has_energy & ~is_guest))
rules.add_rule('can_give_team_member_feedback', team_member & many_members & missing_questionnaire)
rules.add_perm('tcc.receive_peer_feedback_team', team_member & many_members & missing_questionnaire)
rules.add_rule('can_access_full_system', ~is_guest)
