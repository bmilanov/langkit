with Ada.Text_IO; use Ada.Text_IO;

with GNATCOLL.Traces;
with GNATCOLL.VFS; use GNATCOLL.VFS;

with Langkit_Support.Slocs; use Langkit_Support.Slocs;

with Libfoolang.Analysis; use Libfoolang.Analysis;
with Libfoolang.Common;   use Libfoolang.Common;

procedure Main is
   Ctx    : constant Analysis_Context := Create;
   Unit_A : constant Analysis_Unit := Get_From_File (Ctx, "a.txt");
   Unit_B : constant Analysis_Unit := Get_From_File (Ctx, "b.txt");
   Unit_C : constant Analysis_Unit := Get_From_File (Ctx, "b-c.txt");

   procedure Resolve;
   function Visit (Node : Foo_Node'Class) return Visit_Status;
   function Node_Image (Node : Foo_Node'Class) return String;

   -------------
   -- Resolve --
   -------------

   procedure Resolve is
      Dummy : Visit_Status;
   begin
      Put_Line ("Starting resolution...");
      Dummy := Root (Unit_A).Traverse (Visit'Access);
      New_Line;
   end Resolve;

   ----------------
   -- Node_Image --
   ----------------

   function Node_Image (Node : Foo_Node'Class) return String is
   begin
      if Node.Is_Null then
         return "None";
      end if;

      declare
         Fullname : constant String := Get_Filename (Node.Unit);
         Basename : constant String := +Create (+Fullname).Base_Name;
      begin
         return ("<" & Node.Kind_Name & " " & Basename & ":"
                 & Image (Node.Sloc_Range) & ">");
      end;
   end Node_Image;

   -----------
   -- Visit --
   -----------

   function Visit (Node : Foo_Node'Class) return Visit_Status is
   begin
      if not Node.Is_Null and then Node.Kind = Foo_Var then
         declare
            V    : constant Var := Node.As_Var;
            Decl : constant Foo_Node := V.F_Value.P_Resolve;
         begin
            Put_Line ("   " & Node_Image (V) & " -> " & Node_Image (Decl));
         end;
      end if;
      return Into;
   end Visit;

begin
   GNATCOLL.Traces.Parse_Config ("Main_Trace=yes >&1");
   GNATCOLL.Traces.Set_Active (Main_Trace, True);

   Put_Line ("Performing resolution from scratch...");
   Resolve;

   Put_Line ("Performing resolution after reparsing a.txt...");
   Reparse (Unit_A);
   Resolve;

   Put_Line ("Performing resolution after reparsing b.txt...");
   Reparse (Unit_B);
   Resolve;

   Put_Line ("Performing resolution after reparsing b-c.txt...");
   Reparse (Unit_C);
   Resolve;

   Put_Line ("Performing resolution after reparsing b.txt and b-c.txt...");
   Reparse (Unit_B);
   Reparse (Unit_C);
   Resolve;

   Put_Line ("main.adb: Done.");
end Main;
