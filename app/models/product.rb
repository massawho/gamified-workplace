class Product < ApplicationRecord

  scope :is_featured, -> { where(is_featured: true) }

  mount_uploader :photo, ProductUploader

  def unlimited_stock?
    self.stock == -1
  end

  def decrease_stock
    self.stock -= 1 unless unlimited_stock?
  end

  def unlimited_purchase_per_user?
    self.max_per_user == 0
  end

  def can_purchase?(user)
    return true if unlimited_purchase_per_user?
    user.purchases.where(product_id: self.id).count <= self.max_per_user
  end

  def stock_available?
    unlimited_stock? || self.stock > 0
  end
end
