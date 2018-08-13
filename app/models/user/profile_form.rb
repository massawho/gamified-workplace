class User::ProfileForm
  include ActiveModel::Validations

  attr_accessor :name,
    :password,
    :password_confirmation,
    :avatar,
    :username,
    :nickname,
    :date_of_birth

  validates :name, :avatar, :date_of_birth, :password, presence: true

  def initialize user
    @user = user

    @avatar = @user.avatar
    @username = @user.username
    @name = @user.name
    @password = @user.password
    @password_confirmation = @user.password_confirmation
    @nickname = @user.nickname
    @date_of_birth = @user.date_of_birth
  end

  def to_key
    @user.to_key
  end

  def save
    @user.save
  end
end
