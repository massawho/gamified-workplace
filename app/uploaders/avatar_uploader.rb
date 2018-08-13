class AvatarUploader < CarrierWave::Uploader::Base

  include CarrierWave::MiniMagick

  storage :file

  def store_dir
    "uploads/#{model.class.to_s.underscore}/#{mounted_as}/#{model.id}"
  end

  def extension_whitelist
    %w(jpg jpeg gif png)
  end

  version :blurred do
    process :blur, resize_to_fill: [340, 160]
  end

  version :thumb do
    process resize_to_fill: [140, 140]
  end

  def blur(radius=16)
    manipulate! do |img|
      original_path = img.path
      temp_image_path = File.join(Rails.root, 'public', cache_dir, "/blurred_#{File.basename(original_path)}")

      command = "convert #{original_path} -blur 0x#{radius} #{temp_image_path}"
      system(command)

      MiniMagick::Image.open(temp_image_path)
    end
  end
end
