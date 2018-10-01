class HomeController < BaseController

  def index
    @inventory = current_user.purchases.group(:product).count
    @featured_products = Product.accessible_by(current_ability).is_featured
    @goals = Goal.distinct.accessible_by(current_ability).not_accomplished(current_user, Date.today).displayable
    @achievements = current_user.achieved_badges
  end

end
