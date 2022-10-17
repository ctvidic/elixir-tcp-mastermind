
defmodule Player do
  require Logger

  def analyze(line, code) do
    if valid?(line) do
      pick_colors(line, code)
    else
      "Wrong number of colors from client: #{line}"
    end
  end

  def pick_colors(line, code) do
    split_line = String.split(line, "", trim: true)
    split_code = String.split(code, "", trim: true)
    split_line_update = List.flatten(Enum.chunk(split_line, length(split_line)-1))

    correct_location_count = correct_location(split_line, split_code)
    correct_colors_count = correct_colors(split_line, split_code)
    if correct_location_count == 4 and correct_colors_count == 4 do
      "Correctly Guessed! The code was #{code}"
    else
      "Correct Colors: #{correct_colors_count}, Correct Location: #{correct_location_count}, #{code}"
    end
  end

  def correct_colors([], split_code) do
    0
  end

  def correct_location(line, []) do
    0
  end

  def correct_colors([x | rest], split_code) do
    if Enum.member?(split_code, x) do
      1 + correct_colors(rest, split_code)
    else
      correct_colors(rest, split_code)
    end
  end

  def correct_location([x | line_rest], [y | code_rest]) do
    if x == y do
      1 + correct_location(line_rest, code_rest)
    else
      correct_location(line_rest, code_rest)
    end
  end

  def valid?(line) do
    if String.length(line) != 5 do
      false
    else
      true
    end
  end


end

defmodule TcpServer do
  import Player
  require Logger

  @code for _ <- 1..4, into: "", do: <<"#{Enum.random(0..5)}">>

  def accept(port) do
    # The options below mean:
    #
    # 1. `:binary` - receives data as binaries (instead of lists)
    # 2. `packet: :line` - receives data line by line
    # 3. `active: false` - blocks on `:gen_tcp.recv/2` until data is available
    # 4. `reuseaddr: true` - allows us to reuse the address if the listener crashes
    #
    {:ok, socket} =
      :gen_tcp.listen(port, [:binary, packet: :line, active: false, reuseaddr: true])
    Logger.info("Accepting connections on port #{port}")
    loop_acceptor(socket)
  end

  defp loop_acceptor(socket) do
    {:ok, client} = :gen_tcp.accept(socket)
    serve(client)
    loop_acceptor(socket)
  end

  defp serve(socket) do
    socket
    |> read_line()
    |> write_line(socket)

    serve(socket)
  end

  defp read_line(socket) do
    {:ok, data} = :gen_tcp.recv(socket, 0)
    data
  end

  defp write_line(line, socket) do
    :gen_tcp.send(socket, analyze(line, @code))
  end
end
