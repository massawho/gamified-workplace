class AssignmentDeliverable < ApplicationRecord
  belongs_to :exercise
  belongs_to :user

  has_many :answers

  accepts_nested_attributes_for :answers
end
