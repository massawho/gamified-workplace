class BaseController < ApplicationController
  before_action :authenticate_user!
  before_action :check_new_user

  def check_new_user
    return if current_user.nil?
    redirect_to edit_user_path unless current_user.profile_complete?
  end
end
