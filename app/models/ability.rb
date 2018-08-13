class Ability
  include CanCan::Ability

  def initialize(user)
    if user.is_a? User
      active_user_permissions unless user.is_guest?
      user_permissions
    else
      can :manage, :all
    end
  end

  def active_user_permissions
    can :read, Goal
    can :read, Product
    can :recieve_prize, Goal
  end

  def user_permissions
    can :read, Goal, id: Goal.with_exercise
  end
end
