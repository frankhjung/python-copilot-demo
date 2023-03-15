#!/usr/bin/env ruby

# frozen_string_literal: true

# Use public API to read daily astronomy picture.
# See https://go-apod.herokuapp.com/

require "json"
require "net/http"
require "uri"

# Read daily astronomy metadata from go-apod.herokuapp.com.
# Returns:
#     A dictionary of metadata for the daily astronomy image
def get_daily_astronomy_image
  url = "https://go-apod.herokuapp.com/apod"
  uri = URI(url)
  response = Net::HTTP.get_response(uri)
  if response.code != "200"
    puts "Error: status code #{response.code}"
    exit 1
  end
  JSON.parse(response.body)
end

# Read image from url and display to screen.
# Args:
#     url: URL of image to be displayed
def show_image(url)
  # set file name from url
  filename = url.split("/")[-1]
  # stream content from url into a file
  uri = URI(url)
  Net::HTTP.start(uri.host, uri.port, use_ssl: true) do |http|
    request = Net::HTTP::Get.new uri
    http.request request do |response|
      open filename, "wb" do |io|
        response.read_body do |chunk|
          io.write chunk
        end
      end
    end
  end
  # display the file image
  system("display #{filename}")
end

#
# Main
#
# Read daily astronomy image from go-apod.herokuapp.com.
if __FILE__ == $PROGRAM_NAME
  data = get_daily_astronomy_image
  puts data["title"]
  puts data["explanation"]
  show_image(data["url"])
end