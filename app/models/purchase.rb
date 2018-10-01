class Purchase < ApplicationRecord
  belongs_to :product
  belongs_to :user

  before_create :copy_product

  def copy_product
    self.cost = self.product.price
  end
end
