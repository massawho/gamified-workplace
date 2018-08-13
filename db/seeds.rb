AdminUser.create!(email: 'admin@example.com', password: 'password', password_confirmation: 'password') if Rails.env.development?
User.create!(username: '405807', password: 'password', password_confirmation: 'password', department: Department.first, occupation: Occupation.first) if Rails.env.development?
