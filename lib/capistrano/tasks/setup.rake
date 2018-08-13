namespace :setup do
  desc 'Upload .env file to shared folder'
  task :env do
    on roles(:app) do
      upload! fetch(:env_file_path), [shared_path, fetch(:env_file_path)].join('/')
    end
  end

  namespace :check do
    desc 'Task description'
    task :linked_files => fetch(:env_file_path)
  end
end
