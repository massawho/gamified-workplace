class Product < ApplicationRecord

  scope :is_featured, -> { where(is_featured: true) }

  mount_uploader :photo, ProductUploader
end
