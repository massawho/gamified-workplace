class Goal < ApplicationRecord

  include Concerns::Badge

  has_one :exercise
  has_many :achieved_badges

  accepts_nested_attributes_for :achieved_badges

  validates :description, :money, :frequency, :starts_at, :ends_at, :level,
    presence: true
  validate :compatible_dates

  scope :without_exercise, -> { left_outer_joins(:exercise).where(exercises: {id: nil}) }
  scope :with_exercise, -> { joins(:exercise) }
  scope :not_accomplished, -> (user, date) do
    left_outer_joins(achieved_badges: :user)
    .where(achieved_badges: {id: nil})
    .where('achieved_badges.received_at IS NULL
      OR goals.frequency = ?
      OR (EXTRACT(MONTH FROM achieved_badges.received_at) = ? AND goals.frequency = ? )
      OR (EXTRACT(WEEK FROM achieved_badges.received_at) = ? AND goals.frequency = ? )
      OR (achieved_badges.received_at = ? AND goals.frequency = ? )',
      Goal::ONCE,
      date.month, Goal::MONTHLY,
      date.strftime('%W'), Goal::WEEKLY,
      date, Goal::DAILY
      )
  end

  scope :displayable, -> do
    starts_at = Goal.arel_table[:starts_at]
    ends_at = Goal.arel_table[:ends_at]

    where(starts_at.lteq(Date.today))
      .where(ends_at.gteq(Date.today))
      .where(is_active: true)
  end

  ONCE = 1
  DAILY = 2
  WEEKLY = 3
  BIWEEKLY = 4
  MONTHLY = 4

  FREQUENCIES = [
    ['once', Goal::ONCE],
    ['daily', Goal::DAILY],
    ['weekly', Goal::WEEKLY],
    ['biweekly', Goal::BIWEEKLY],
    ['monthly', Goal::MONTHLY]
  ]

  def readable_frequency
    Goal::FREQUENCIES.each do |l|
      return l[0] if l[1] === self.frequency
    end
  end

  def once?
    self.frequency == Goal::ONCE
  end

  def to_s
    "##{self.id} #{self.description}"
  end

  private

  def compatible_dates
    self.errors.add(:ends_at, 'cannot be before start date') if self.ends_at < self.starts_at
  end

end
