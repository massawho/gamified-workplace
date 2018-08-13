ActiveAdmin.register Product do
  permit_params :name, :price, :description, :stock, :max_per_user, :is_active,
    :is_featured, :photo

end
