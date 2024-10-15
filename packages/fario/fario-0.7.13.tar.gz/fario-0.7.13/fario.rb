class Fario < Formula
  include Language::Python::Virtualenv
  desc "Command-line tools for Farcaster power users"
  homepage "https://github.com/vrypan/fario"
  url "https://files.pythonhosted.org/packages/19/d0/6adc26c70c17834e2ab2fa9dedbe77caa3529e75e2e7efaa2207b634d86a/fario-0.7.12.tar.gz"
  sha256 "094f69b8fc4a2aabdb0cbeecf552afedfb788b12c9f050da02c1ab792eecfbec"
  license "MIT"

  bottle do
   rebuild 1
   root_url "https://raw.githubusercontent.com/vrypan/homebrew-fario/main"
   sha256 cellar: :any, arm64_sonoma: "cea66be6a21406d34a0199404ffbab8a3c204e6f8676ae9ca2db2983b6b9264e"
  end

  livecheck do
    url :stable
  end

  depends_on "rust" => [:build]
  depends_on "protobuf"
  depends_on "python@3.12"

  resource "fario" do
    url "https://files.pythonhosted.org/packages/19/d0/6adc26c70c17834e2ab2fa9dedbe77caa3529e75e2e7efaa2207b634d86a/fario-0.7.12.tar.gz"
    sha256 "094f69b8fc4a2aabdb0cbeecf552afedfb788b12c9f050da02c1ab792eecfbec"
  end

  def install
    virtualenv_install_with_resources
  end
end