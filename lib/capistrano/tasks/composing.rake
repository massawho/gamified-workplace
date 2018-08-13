namespace :composing do
  desc "Build application images"
  task :build do
    on roles(:app) do
      within current_path do
        execute("docker-compose",
          "-f", "#{fetch(:docker_file_path)}/docker-compose.#{fetch(:stage)}.yaml",
          "build"
        )
      end
    end
  end

  desc "Take down compose application containers"
  task :down do
    on roles(:app) do
      within current_path do
        execute("docker-compose",
          "-f", "#{fetch(:docker_file_path)}/docker-compose.#{fetch(:stage)}.yaml",
          "down"
        )
      end
    end
  end

  namespace :restart do
    desc "Rebuild and restart app container"
    task :app do
      on roles(:app) do
        within current_path do
          execute("docker-compose",
            "-f", "#{fetch(:docker_file_path)}/docker-compose.#{fetch(:stage)}.yaml",
            "build"
          )
          execute("docker-compose",
            "-f", "#{fetch(:docker_file_path)}/docker-compose.#{fetch(:stage)}.yaml",
            "up", "-d", "app"
          )
        end
      end
    end
    desc "Rebuild and restart nginx container"
    task :nginx do
      on roles(:app) do
        within current_path do
          execute("docker-compose",
            "-f", "#{fetch(:docker_file_path)}/docker-compose.#{fetch(:stage)}.yaml",
            "up", "-d", "--force-recreate", "nginx"
          )
        end
      end
    end
    desc "Rebuild and restart sidekiq container"
    task :sidekiq do
      on roles(:app) do
        within current_path do
          execute("docker-compose",
            "-f", "#{fetch(:docker_file_path)}/docker-compose.#{fetch(:stage)}.yaml",
            "up", "-d", "--force-recreate", "sidekiq"
          )
        end
      end
    end
  end

  namespace :database do
    desc "Up database and make sure it's ready"
    task :up do
      on roles(:app) do
        within current_path do
          execute("docker-compose",
            "-f", "#{fetch(:docker_file_path)}/docker-compose.#{fetch(:stage)}.yaml",
            "up", "-d", "--no-deps", "postgres"
          )
        end
      end
      sleep 5
    end

    desc "Create database"
    task :create do
      on roles(:app) do
        within current_path do
          execute("docker-compose",
            "-f", "#{fetch(:docker_file_path)}/docker-compose.#{fetch(:stage)}.yaml",
            "run", "--rm", "app", "bundle", "exec", "rake", "db:create"
          )
        end
      end
    end

    desc "Migrate database"
    task :migrate do
      on roles(:app) do
        within current_path do
          execute("docker-compose",
            "-f", "#{fetch(:docker_file_path)}/docker-compose.#{fetch(:stage)}.yaml",
            "run", "--rm", "app", "bundle", "exec", "rake", "db:migrate"
          )
        end
      end
    end
  end

  namespace :assets do
    desc "Precompile assets"
    task :precompile do
      on roles(:app) do
        within current_path do
          execute("docker-compose",
            "-f", "#{fetch(:docker_file_path)}/docker-compose.#{fetch(:stage)}.yaml",
            "run", "-v", "gamified-workplace_public:/app/public", "--rm", "app", "bundle", "exec", "rake", "assets:precompile"
          )
        end
      end
    end
  end
end
