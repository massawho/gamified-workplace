# config valid for current version and patch releases of Capistrano
lock "~> 3.11.0"

set :application, "gamified-workplace"
set :repo_url, "git@github.com:massa1240/gamified-workplace.git"
set :branch, "rails-master"

# Default branch is :master
# ask :branch, `git rev-parse --abbrev-ref HEAD`.chomp

set :deploy_to, "/opt/gamified-workplace/production"

# Default value for :format is :airbrussh.
# set :format, :airbrussh

# You can configure the Airbrussh format using :format_options.
# These are the defaults.
# set :format_options, command_output: true, log_file: "log/capistrano.log", color: :auto, truncate: :auto

# Default value for :pty is false
# set :pty, true

# Default value for :linked_files is []
# append :linked_files, "config/database.yml"

# Default value for linked_dirs is []
# append :linked_dirs, "log", "tmp/pids", "tmp/cache", "tmp/sockets", "public/system"

# Default value for default_env is {}
# set :default_env, { path: "/opt/ruby/bin:$PATH" }

# Default value for local_user is ENV['USER']
# set :local_user, -> { `git config user.name`.chomp }

# Default value for keep_releases is 5
# set :keep_releases, 5

# Uncomment the following to require manually verifying the host key before first deploy.
# set :ssh_options, verify_host_key: :secure


namespace :deploy do
  desc "Initialize application"
  task :initialize do
    invoke 'composing:build'
    invoke 'composing:database:up'
    invoke 'composing:database:create'
    invoke 'composing:database:migrate'
  end

  after :published, :restart do
    invoke 'composing:restart:app'
    invoke 'composing:restart:sidekiq'
    invoke 'composing:restart:nginx'
    invoke 'composing:assets:precompile'
    invoke 'composing:database:migrate'
  end

  before :finished, :clear_containers do
    on roles(:app) do
      execute "docker ps -a -q -f status=exited | xargs -r docker rm -v"
      execute "docker images -f dangling=true -q | xargs -r docker rmi -f"
    end
  end
end
