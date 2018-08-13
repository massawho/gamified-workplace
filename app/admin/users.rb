ActiveAdmin.register User do
  permit_params :name, :password, :password_confirmation, :occupation_id,
    :department_id, :is_guest, :date_of_birth, :avatar, :username, :nickname

  index do
    selectable_column
    column :name
    column :email
    column :current_sign_in_at
    column :sign_in_count
    column :created_at
    actions
  end

  filter :email
  filter :current_sign_in_at
  filter :sign_in_count
  filter :created_at

  form do |f|
    f.inputs 'Login information' do
      f.input :username
      f.input :password
      f.input :is_guest
      f.input :password_confirmation
    end
    f.inputs 'User info' do
      f.input :name
      f.input :nickname
      f.input :department
      f.input :occupation
      f.input :date_of_birth, as: :string
      f.input :avatar
    end
    f.actions
  end
end
