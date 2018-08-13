class AchievedBadge < ApplicationRecord

  include Concerns::Badge

  delegate :description, to: :goal

  belongs_to :user
  belongs_to :goal

  validate :correctness_of_received_at

  before_create :populate_values
  before_create :award_prize

  private

  def award_prize
    self.money = self.user.award_prize(self.goal)
    self.user.save!
  end

  def populate_values
    self.level = goal.level
  end

  def correctness_of_received_at
    self.errors.add(
      :received_at,
      'user has already received this achivement in this range of date'
      ) unless Goal.where(id: self.goal.id).not_accomplished(self.user, self.received_at).exists?
  end
end
