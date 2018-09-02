class Exercise < ApplicationRecord

  attr_writer :level, :money

  validates :level, :money, presence: true, unless: :goal_present?
  validates :due_at, presence: true

  belongs_to :goal, dependent: :delete
  has_many :questions, dependent: :delete_all
  has_many :assignment_deliverables

  accepts_nested_attributes_for :questions, :allow_destroy => true
  accepts_nested_attributes_for :goal, :allow_destroy => true

  before_validation :create_goal

  def money
    self.goal.try(:money)
  end

  def level
    self.goal.try(:level)
  end

  def to_s
    description
  end

  private

  def create_goal
    unless goal_present?
      self.goal = Goal.new
      self.goal.is_active = true
      self.goal.frequency = Goal::ONCE
      self.goal.starts_at = Date.today
    end

    self.goal.level = @level if @level.present?
    self.goal.money = @money if @money.present?
    self.goal.description = self.description if self.description_changed?
    self.goal.ends_at = self.due_at if self.due_at_changed?

  end

  def goal_present?
    self.goal.present?
  end
end
