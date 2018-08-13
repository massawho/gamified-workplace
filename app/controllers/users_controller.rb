class UsersController < BaseController

  skip_before_action :check_new_user, only: [:edit, :update]

  def edit
  end

  def update
    current_user.attributes = user_parameters
    context = if current_user.profile_complete?
      :update_profile
    else
      :first_login
    end

    if current_user.save(context: context)
      redirect_to :root
    else
      render :edit
    end
  end

  protected

  def user_parameters
    params.require(:user).permit(:name, :password, :password_confirmation,
      :avatar, :username, :nickname, :date_of_birth
    )
  end
end
