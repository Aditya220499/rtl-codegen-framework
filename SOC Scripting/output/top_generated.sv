// AUTO-GENERATED FILE
// Do not edit manually

module top;

logic clk;
logic rst_n;
logic irq;
logic [31:0] addr;
logic [31:0] wdata;
logic ready;


// Instance: u_cpu
cpu_core u_cpu (
.clk(clk),
.rst_n(rst_n),
.irq(irq),
.addr(addr),
.wdata(wdata),
.ready(ready)

);

// Instance: u_mem
memory_ctrl u_mem (
.clk(clk),
.rst_n(rst_n),
.addr(addr),
.wdata(wdata),
.ready(ready)

);

// Instance: u_uart
uart u_uart (
.clk(clk),
.rst_n(rst_n),
.irq(irq)

);

endmodule