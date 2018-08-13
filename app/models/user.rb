class User < ApplicationRecord
  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable and :omniauthable
  devise :database_authenticatable,
         :recoverable, :rememberable, :trackable,
         authentication_keys: [:username]

  belongs_to :department
  belongs_to :occupation
  has_many :assignment_deliverables
  has_many :achieved_badges

  validates :username, presence: true, uniqueness: true
  validates :name, :avatar, :date_of_birth, :password, presence: true, on: :first_login
  validates :name, :avatar, :date_of_birth, presence: true, on: :update_profile

  mount_uploader :avatar, AvatarUploader

  def display_name
    return nickname unless nickname.empty?
    return name unless name.empty?
    username
  end

  def has_started?(exercise)
    assignment_deliverables.where(user: self, exercise: exercise).exists?
  end

  def profile_complete?
    date_of_birth.present? && name.present? && username.present?
  end

  def award_prize(goal)
    if !self.is_guest?
      self.money = 0 if self.money.nil?
      self.money += goal.money
      goal.money
    else
      0
    end
  end

end
