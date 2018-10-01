class AssignmentDeliverable < ApplicationRecord
  belongs_to :exercise
  belongs_to :user

  has_many :answers

  scope :correction_completed, -> do
    where(correction_completed: true)
  end

  accepts_nested_attributes_for :answers
end
