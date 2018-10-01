class Ability
  include CanCan::Ability

  def initialize(user)
    if user.is_a? User
      active_user_permissions(user) unless user.is_guest?
      user_permissions(user)
    else
      can :manage, :all
    end
  end

  def active_user_permissions(user)
    can :read, Goal
    can :read, Product
    can :recieve_prize, Goal
  end

  def user_permissions(user)
    can :read, Goal, id: Goal.with_exercise
    can :manage, AssignmentDeliverable, user_id: user.id
  end
end
