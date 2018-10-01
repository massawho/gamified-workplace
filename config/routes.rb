Rails.application.routes.draw do
  devise_for :admin_users, ActiveAdmin::Devise.config
  ActiveAdmin.routes(self)
  devise_for :users, controllers: {
    sessions: 'users/sessions'
  }
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html

  root to: 'home#index'

  resources :products, only: [:index]
  resources :purchases, only: [:create]
  resource :user, only: [:edit, :update]
  resources :assignment_deliverables, only: [:create, :edit, :update]
end
