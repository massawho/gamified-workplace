class Exercise::DownloadService

  require 'zip'

  def initialize(zipfile_name = nil)
    @zipfile_name = zipfile_name || '/tmp/archive.zip'
  end

  def create_downloadable_file(exercise)
    File.delete(@zipfile_name) if File.file?(@zipfile_name)

    Zip::File.open(@zipfile_name, Zip::File::CREATE) do |zipfile|
      exercise.assignment_deliverables.each do |assignment|

        username = assignment.user.username
        assignment.answers.each do |answer|
          # - The name of the file as it will appear in the archive
          # - The original file, including the path to find it
          unless answer.upload.file.nil?
            extension = answer.upload.file.extension
            folder = "#{username}/#{answer.file_name}.#{extension}"
            zipfile.add(folder, answer.upload.file.path)
          end
        end
      end
    end
    @zipfile_name
  end
end
